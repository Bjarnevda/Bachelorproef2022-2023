interface PaginateProps {
  articlesPerPage: number;
  totalArticles: number;
  indexOfFirstArticle: number;
  indexOfLastArticle: number;
  currentPage: number;
  paginate: any;
}

export default function Paginate({
  articlesPerPage,
  totalArticles,
  paginate,
  indexOfFirstArticle,
  indexOfLastArticle,
  currentPage,
}: PaginateProps) {
  const pageNumbers = [];

  for (let i = 1; i <= Math.ceil(totalArticles / articlesPerPage); i++) {
    pageNumbers.push(i);
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
            <li
              className="page-item"
              onClick={() => paginate(currentPage - 1)}
            >
              <a className="page-link">
                <span aria-hidden="true">&laquo;</span>
                <span className="sr-only">Previous</span>
              </a>
            </li>

            {pageNumbers.map((number) => (
              <li
                key={number}
                className="page-item"
                onClick={() => paginate(number)}
              >
                <a className="page-link">{number}</a>
              </li>
            ))}

            <li
              className="page-item"
              onClick={() => paginate(currentPage + 1)}
            >
              <a className="page-link">
                <span aria-hidden="true">&raquo;</span>
                <span className="sr-only">Next</span>
              </a>
            </li>
          </ul>
        </nav>
      </div>
    </div>
  );
};