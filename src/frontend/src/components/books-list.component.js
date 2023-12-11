import React, { Component } from "react";
import { Link } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import http from "../http-common";

export default class BooksList extends Component {
  constructor(props) {
    super(props);
    this.handleChange = this.handleChange.bind(this);
    this.handleKeyDown = this.handleKeyDown.bind(this);
    this.retrieveBooks = this.retrieveBooks.bind(this);
    this.refreshList = this.refreshList.bind(this);
    this.setActiveBook = this.setActiveBook.bind(this);
    this.searchQuery = this.searchQuery.bind(this);

    this.state = {
      books: [],
      currentBook: null,
      currentIndex: -1,
      searchQuery: "",
    };
  }

  componentDidMount() {
    this.retrieveBooks();
  }

  handleChange = (event) => {
    const { name, value } = event.target;

    this.setState({
      [name]: value,
    });
  };

  retrieveBooks() {
    http
      .get(`/books`)
      .then((response) => {
        this.setState({
          books: response.data.data,
        });
        console.log(response.data);
      })
      .catch((e) => {
        this.setState({
          books: [],
          currentBook: null,
          currentIndex: -1,
        });
        console.log(e);
      });
  }

  refreshList() {
    this.retrieveBooks();
    this.setState({
      currentBook: null,
      currentIndex: -1,
    });
  }

  setActiveBook(book, index) {
    console.log(book);
    this.setState({
      currentBook: book,
      currentIndex: index,
    });
  }

  searchQuery() {
    http
      .get(`/books?q=${this.state.searchQuery}`)
      .then((response) => {
        this.setState({
          books: response.data.data,
        });
        console.log(response.data);
      })
      .catch((e) => {
        console.log(e);
        this.setState({
          books: [],
          currentBook: null,
          currentIndex: -1,
        });
      });
  }

  handleKeyDown = (event) => {
    if (event.key === "Enter") {
      this.searchQuery();
    }
  };

  render() {
    const { searchQuery, books, currentBook, currentIndex } = this.state;

    return (
      <div className="row">
        <div className="col-12">
          <div className="row">
            <div className="col input-group mb-3">
              <input
                name="searchQuery"
                type="text"
                className="form-control"
                placeholder="Search books by name, authors, summary or publication year"
                value={searchQuery}
                onChange={this.handleChange}
                onKeyDown={this.handleKeyDown}
              />
              <div className="input-group-append">
                <button
                  className="btn btn-primary"
                  type="button"
                  onClick={this.searchQuery}
                >
                  Search
                </button>
              </div>
            </div>
          </div>
          <div className="row">
            <div className="col-md-6">
              <div>
                <div className="row align-items-center justify-content-between">
                  <div className="col-5">
                    <h4>{books.length} Books found</h4>
                  </div>
                  <div className="col-2">
                    <Link to={"/add"} className="btn btn-success">
                      Add book
                    </Link>
                  </div>
                </div>
                {books.length > 0 ? (
                  <div>
                    <small>Click on a book to view it</small>
                    <ul className="list-group">
                      {books.map((book, index) => (
                        <li
                          className={
                            "list-group-item " +
                            (index === currentIndex ? "active" : "")
                          }
                          onClick={() => this.setActiveBook(book, index)}
                          key={index}
                        >
                          {book.title}
                        </li>
                      ))}
                    </ul>
                  </div>
                ) : (
                  <div></div>
                )}
              </div>
            </div>
            <div className="col-md-6">
              {currentBook ? (
                <div className="card">
                  <div className="card-header">
                    <strong>{currentBook.title}</strong>
                  </div>
                  <div className="card-body">
                    <p className="card-text">
                      <strong>Authors: </strong>
                      {currentBook.authors}
                    </p>
                    <p className="card-text">
                      <strong>Summary: </strong>
                      {currentBook.summary}
                    </p>
                    <p className="card-text">
                      <strong>Publication Year: </strong>
                      {currentBook.publication_year}
                    </p>
                    <Link
                      to={"/books/" + currentBook.id}
                      className="btn btn-sm btn-primary"
                    >
                      Edit
                    </Link>
                  </div>
                </div>
              ) : (
                <div></div>
              )}
            </div>
          </div>
        </div>
      </div>
    );
  }
}
