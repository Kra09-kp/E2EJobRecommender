from src.jobRecommender.mcp.mcp_server import mcp


def main():
    print("Hello from e2e-job-recommender!")
    print("If you see this message, then read the readme file and try again :)")
    mcp.run(transport='stdio')


if __name__ == "__main__":
    main()
