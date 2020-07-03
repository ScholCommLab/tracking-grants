import pandas as pd

from tracking_grants import (
    articles_f,
    references_f,
    wos_f,
    altmetric_f,
    trials_f,
    awards_f,
)


def load_references():
    return pd.read_csv(references_f)


def load_awards():
    def research_topic(s):
        if pd.notna(s):
            primary_topic = None
            secondary_topic = None

            if "Secondary: " in s:
                splits = s.split("Secondary: ")
                secondary_topic = splits[-1]
                s = splits[0:-1][0]
            if "Primary: " in s:
                splits = s.split("Primary: ")
                primary_topic = splits[-1]
            return primary_topic, secondary_topic
        else:
            return None, None

    def currency_to_int(s):
        s = s.replace("$", "").replace(",", "")
        return int(float(s))

    awards = pd.read_csv(awards_f)
    awards = awards.rename(
        columns={
            "Award Amount": "award_amount",
            "Fiscal Year": "award_year",
            "Mechanism": "type",
            "Proposal Number": "grant_id",
            "Award Number": "award_number",
            "Program": "program",
        }
    )
    awards[["primary_topic", "secondary_topic"]] = pd.DataFrame(
        awards["Research Topic"].map(research_topic).tolist()
    )
    awards = awards.drop(columns=["Research Topic"])
    awards["award_amount"] = awards["award_amount"].map(currency_to_int)

    export_cols = [
        "award_id",
        "grant_id",
        "award_amount",
        "award_year",
        "type",
        "program",
        "primary_topic",
        "secondary_topic",
    ]
    return awards[export_cols]


# Loading external files
def load_articles():
    return pd.read_csv(articles_f)


def load_wos():
    # Load metrics from WoS
    wos = pd.read_csv(wos_f, low_memory=False, index_col="DOI")
    wos.columns = [x.lower() for x in wos.columns.tolist()]
    wos.index = wos.index.str.lower()

    wos = wos.rename(
        columns={
            "citations": "wos_citations",
            "relative citation score": "citation_score",
        }
    )
    return wos


def load_altmetrics(keep_metrics=True, keep_dates=False, keep_ids=False):
    altmetrics = pd.read_json(altmetric_f).T

    # Filter out all articles had not altmetrics
    altmetrics = altmetrics[altmetrics.altmetric_id.notna()]

    # Transform all DOIs to lowercase
    altmetrics.index = altmetrics.index.str.lower()

    cols_to_keep = []

    if keep_metrics:
        metric_cols = {
            "cited_by_posts_count": "posts_count",
            "cited_by_rh_count": "research_highlight",
            "cited_by_tweeters_count": "twitter_accounts",
            "cited_by_patents_count": "patents",
            "cited_by_msm_count": "news_outlets",
            "cited_by_feeds_count": "blogs",
            "cited_by_fbwalls_count": "fb_pages",
            "cited_by_qna_count": "stackoverflow",
            "cited_by_videos_count": "videos",
            "cited_by_peer_review_sites_count": "peer_reviews",
            "cited_by_weibo_count": "weibo",
            "cited_by_gplus_count": "gplus",
            "cited_by_rdts_count": "reddit_threads",
            "cited_by_policies_count": "policies",
            "cited_by_syllabi_count": "syllabi",
            "cited_by_linkedin_count": "linkedin",
            "cited_by_wikipedia_count": "wikipedia",
        }
        altmetrics = altmetrics.rename(columns=metric_cols)
        metric_cols = list(metric_cols.values())

        altmetrics[metric_cols] = altmetrics[metric_cols].astype(float)
        cols_to_keep = cols_to_keep + metric_cols

    if keep_dates:
        dates = ["last_updated", "published_on", "added_on"]
        for d in dates:
            altmetrics[d] = pd.to_datetime(altmetrics[d], unit="s")
        cols_to_keep = cols_to_keep + dates

    if keep_ids:
        id_cols = ["pmid", "pmc", "altmetric_id", "doi", "hollis_id", "arxiv_id"]
        for _ in id_cols:
            altmetrics[_] = altmetrics[_].astype(str)
        cols_to_keep = cols_to_keep + id_cols

    return altmetrics[cols_to_keep]


def load_metrics():
    articles = load_articles()

    trials = load_trials()

    articles = articles.merge(
        trials.doi.value_counts().to_frame("n_trials"),
        left_on="DOI",
        right_index=True,
        how="left",
    )

    return articles


def load_trials():
    return pd.read_csv(trials_f)
