import os
import json
from typing import Union, Any
from github import Github
from github import RateLimitExceededException
from datetime import datetime, timedelta
import pandas as pd


def info(event, context):
    access_token = os.environ.get("GITHUB_ACCESS_TOKEN")
    g: object = Github(access_token, per_page=100)

    repositories: list[Union[str, Any]] = [
        "ethereum/go-ethereum",
        "solana-labs/solana",
        "maticnetwork/bor",
        "paritytech/polkadot",
        "cosmos/cosmos-sdk",
        "algorand/go-algorand",
        "ava-labs/avalanchego",
        "input-output-hk/cardano-node",
        "EOSIO/eos",
        "vechain/thor",
        "ethereum-optimism/optimism",
        "OffchainLabs/arbitrum"
    ]

    data: dict[str, list[Any]] = {'Repository': [], 'Number of contributors': [],
                                  'Number of releases in the past year': []}

    for repo_name in repositories:
        try:
            repo = g.get_repo(repo_name)

            contributors = repo.get_contributors()
            contributors_count = contributors.totalCount

            one_year_ago = datetime.now() - timedelta(days=365)

            releases = repo.get_releases()
            yearly_releases = 0

            for release in releases:
                release_date = release.published_at

                if release_date > one_year_ago:
                    yearly_releases += 1
                elif release_date < one_year_ago:
                    break

            data['Repository'].append(repo_name)
            data['Number of contributors'].append(contributors_count)
            data['Number of releases in the past year'].append(yearly_releases)

        except RateLimitExceededException:
            rate_limit_reset_time = g.rate_limiting_resettime
            current_time = datetime.now().timestamp()
            sleep_time = max(rate_limit_reset_time - current_time, 0)

            return {
                'statusCode': 429,
                'body': json.dumps({
                    'message': f"Rate limit exceeded. Please wait for {sleep_time} seconds for the rate limit to reset."
                })
            }

    df = pd.DataFrame(data, columns=['Repository', 'Number of contributors', 'Number of releases in the past year'])

    return {
        'statusCode': 200,
        'body': json.dumps(df.to_dict(orient='records'))
    }
