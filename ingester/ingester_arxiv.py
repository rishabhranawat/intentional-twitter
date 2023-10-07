import arxiv

# Define the file where you want to write the results
output_file = "arxiv_results.txt"

# Open the file in write mode
with open(output_file, "w", encoding="utf-8") as file:
    search = arxiv.Search(
        query="quantum",
        max_results=10,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )

    for result in search.results():
        data = f'Title: {result.title}\nAuthors: {result.authors}\nSummary: {result.summary}\nPublished On: {result.published}\nCategory: {result.primary_category}\n\n'
        file.write(data)

print(f"Results written to {output_file}")
