import http from "../http-common";

class BookDataService {
    get(id) {
        return http.get(`/books/${id}`);
    }

    create(data) {
        return http.post("/books", data);
    }

    update(id, data) {
        return http.put(`/books/${id}`, data);
    }

    delete(id) {
        return http.delete(`/books/${id}`);
    }

    search(q) {
        return http.get(`/books?q=${q}`);
    }
}

const bookDataService = new BookDataService();
export default bookDataService;
