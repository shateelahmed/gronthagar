import React, { Component } from "react";
import http from "../http-common";
import { withRouter } from "../common/with-router";
import "bootstrap/dist/css/bootstrap.min.css";

class Book extends Component {
  constructor(props) {
    super(props);
    this.handleChange = this.handleChange.bind(this);
    this.handleKeyDown = this.handleKeyDown.bind(this);
    this.getBook = this.getBook.bind(this);
    this.updateBook = this.updateBook.bind(this);
    this.deleteBook = this.deleteBook.bind(this);

    this.state = {
      book: {
        id: null,
        title: "",
        authors: "",
        summary: "",
        publication_year: "",
      },
      alertType: "",
      message: "",
    };
  }

  componentDidMount() {
    this.getBook(this.props.router.params.id);
  }

  handleChange = (event) => {
    const { name, value } = event.target;

    this.setState(function (previousState) {
      return {
        book: {
          ...previousState.book,
          [name]: value,
        },
      };
    });
  };

  getBook(id) {
    http
      .get(`/books/${id}`)
      .then((response) => {
        this.setState({
          book: response.data.data,
        });
      })
      .catch((e) => {
        console.log(e);
      });
  }

  updateBook() {
    http
      .put(`/books/${this.state.book.id}`, this.state.book)
      .then((response) => {
        this.setState({
          alertType: "success",
          message: "Book updated successfully",
        });
      })
      .catch((e) => {
        console.log(e);
        if (e.response.status !== undefined && e.response.status === 422) {
          this.setState({
            alertType: "danger",
            message: "All fields are required and the field Publication Year must be a valid year",
          });
        }
      });
  }

  handleKeyDown = (event) => {
    if (event.key === "Enter") {
      this.updateBook();
    }
  };

  deleteBook() {
    http
      .delete(`/books/${this.state.book.id}`)
      .then((response) => {
        this.props.router.navigate("/books");
      })
      .catch((e) => {
        console.log(e);
      });
  }

  render() {
    const { book, message, alertType } = this.state;

    return (
      <div className="card p-3">
        {book ? (
          <div className="edit-form">
            <h4>Edit Book</h4>
            {message ? (
              <div className={`alert alert-${alertType}`} role="alert">
                {message}
              </div>
            ) : (
              <div></div>
            )}
            <form>
              <div className="form-group mb-2">
                <label htmlFor="title">Title</label>
                <input
                  type="text"
                  className="form-control"
                  id="title"
                  value={book.title}
                  onChange={this.handleChange}
                  onKeyDown={this.handleKeyDown}
                  name="title"
                />
              </div>
              <div className="form-group mb-2">
                <label htmlFor="authors">Authors</label>
                <input
                  type="text"
                  className="form-control"
                  id="authors"
                  value={book.authors}
                  onChange={this.handleChange}
                  onKeyDown={this.handleKeyDown}
                  name="authors"
                />
              </div>
              <div className="form-group mb-2">
                <label htmlFor="summary">Summary</label>
                <input
                  type="text"
                  className="form-control"
                  id="summary"
                  value={book.summary}
                  onChange={this.handleChange}
                  onKeyDown={this.handleKeyDown}
                  name="summary"
                />
              </div>
              <div className="form-group mb-2">
                <label htmlFor="publicationYear">Publication Year</label>
                <input
                  type="text"
                  className="form-control"
                  id="publicationYear"
                  value={book.publication_year}
                  onChange={this.handleChange}
                  onKeyDown={this.handleKeyDown}
                  name="publication_year"
                />
              </div>
            </form>

            <div className="mt-3">
              <button
                type="submit"
                className="btn btn-sm btn-success"
                onClick={this.updateBook}
              >
                Update
              </button>
              &nbsp;
              <button
                className="btn btn-sm btn-danger"
                onClick={this.deleteBook}
              >
                Delete
              </button>
            </div>
          </div>
        ) : (
          <div></div>
        )}
      </div>
    );
  }
}

export default withRouter(Book);
