import React, { Component } from "react";
import http from "../http-common";

export default class AddBook extends Component {
  initialState = {
    book: {
      id: null,
      title: "",
      authors: "",
      summary: "",
      publicationYear: "",
    },
    message: "",
  };

  constructor(props) {
    super(props);
    this.handleChange = this.handleChange.bind(this);
    this.handleKeyDown = this.handleKeyDown.bind(this);
    this.saveBook = this.saveBook.bind(this);

    this.state = this.initialState;
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

  saveBook() {
    const data = {
      title: this.state.book.title,
      authors: this.state.book.authors,
      summary: this.state.book.summary,
      publication_year: this.state.book.publicationYear,
    };

    http
      .post("/books", data)
      .then((response) => {
        this.setState(this.initialState);
        this.setState({
          message: "Book added successfully",
        });
        console.log(response.data);
      })
      .catch((e) => {
        console.log(e);
      });
  }

  handleKeyDown = (event) => {
    if (event.key === "Enter") {
      this.saveBook();
    }
  };

  render() {
    const { book, message } = this.state;
    return (
      <div className="card p-3">
        <h4>Add Book</h4>
        {message ? (
          <div className="alert alert-success" role="alert">
            {message}
          </div>
        ) : (
          <div></div>
        )}
        <div className="form-group mb-2">
          <label htmlFor="title">Title</label>
          <input
            type="text"
            className="form-control"
            id="title"
            required
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
            required
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
            required
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
            required
            value={book.publicationYear}
            onChange={this.handleChange}
            onKeyDown={this.handleKeyDown}
            name="publicationYear"
          />
        </div>

        <div className="mt-3">
          <button className="btn btn-success" onClick={this.saveBook}>
            Submit
          </button>
        </div>
      </div>
    );
  }
}
