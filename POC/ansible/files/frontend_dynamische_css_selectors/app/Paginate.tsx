interface PaginateProps {
  articlesPerPage: number;
  totalArticles: number;
  indexOfFirstArticle: number;
  indexOfLastArticle: number;
  currentPage: number;
  previousPage: number;
  nextPage: number;
}

export default function Paginate({
  articlesPerPage,
  totalArticles,
  indexOfFirstArticle,
  indexOfLastArticle,
  previousPage,
  nextPage,
}: PaginateProps) {
  const pageNumbers = [];

  for (let i = previousPage - 1; i <= Math.ceil(nextPage + 1); i++) {
    if (i > 0 && i <= Math.ceil(totalArticles / articlesPerPage)) {
      pageNumbers.push(i);
    }
  }

  if (indexOfLastArticle > totalArticles) {
    indexOfLastArticle = totalArticles;
  }

  return (
    <div className="pagination-container">
      <div className="pagination-wrapper float-left w-100">
        <p>
          Showing {indexOfFirstArticle + 1} to {indexOfLastArticle} out of{" "}
          {totalArticles} ({Math.ceil(totalArticles / articlesPerPage)} Pages)
        </p>
        <nav aria-label="Page navigation example">
          <ul className="pagination">
            <li className="page-item">
              <a className="page-link" href={`/?page=${1}`}>
                <span aria-hidden="true">&laquo;</span>
                <span className="sr-only">First</span>
              </a>
            </li>
            <li className="page-item">
              <a className="page-link" href={`/?page=${previousPage}`}>
                <span aria-hidden="true">&laquo;</span>
                <span className="sr-only">Previous</span>
              </a>
            </li>
            {pageNumbers.map((number) => (
              <li key={number} className="page-item">
                <a className="page-link" href={`/?page=${number}`}>
                  {number}
                </a>
              </li>
            ))}

            <li className="page-item">
              <a className="page-link" href={`/?page=${nextPage}`}>
                <span aria-hidden="true">&raquo;</span>
                <span className="sr-only">Next</span>
              </a>
            </li>

            <li className="page-item">
              <a
                className="page-link"
                href={`/?page=${Math.ceil(totalArticles / articlesPerPage)}`}
              >
                <span aria-hidden="true">&raquo;</span>
                <span className="sr-only">Last</span>
              </a>
            </li>
          </ul>
        </nav>
      </div>
    </div>
  );
}
