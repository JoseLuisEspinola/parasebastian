const moviesForm = document.querySelector("#form-registro");

function addMovieRow(
  movieId,
  titulo,
  sinopsis,

  url_pelicula,
  ano_extreno,
  duracion,
  categoria,
  actor,
  director
) {
  const tableBody = document.querySelector("#tabla-peliculas tbody");

  const row = document.createElement("tr");
  row.id = `movie-${movieId}`;
  row.innerHTML = `
        <td>${titulo}</td>
        <td>${sinopsis}</td>
        <td>${url_pelicula}</td>
        <td>${ano_extreno}</td>
        <td>${duracion}</td>
        <td>${categoria}</td>
        <td>${actor}</td>
        <td>${director}</td>
        <td>
            <button class="btn btn-danger btn-sm delete-btn">Eliminar</button>
            <button class="btn btn-warning btn-sm edit-btn">Editar</button>
        </td>
    `;

  const deleteButton = row.querySelector(".delete-btn");
  deleteButton.addEventListener("click", async () => {
    const response = await fetch(`/api/movies/${movieId}`, {
      method: "DELETE",
    });
    const data = await response.json();
    rmMovieRow(data.id_pelicula);
  });
  tableBody.appendChild(row);

  const editButton = row.querySelector(".edit-btn");
  editButton.addEventListener("click", async () => {
    moviesForm["movieId"].value = movieId;
    moviesForm["titulo"].value = titulo;
    moviesForm["sinopsis"].value = sinopsis;
    moviesForm["url_pelicula"].value = url_pelicula;
    moviesForm["ano_extreno"].value = ano_extreno;
    moviesForm["duracion"].value = duracion;
    moviesForm["genero"].value = genero;
    moviesForm["categoria"].value = categoria;
    moviesForm["actor"].value = actor;
    moviesForm["director"].value = director;
    
  });
  tableBody.appendChild(row);
}

function rmMovieRow(movieId) {
  const row = document.querySelector(`#movie-${movieId}`);
  row.remove();
}

moviesForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const movieId = moviesForm["movieId"].value;
  const titulo = moviesForm["titulo"].value;
  const sinopsis = moviesForm["sinopsis"].value;
  const url_pelicula = moviesForm["url_pelicula"].value;
  const ano_extreno = moviesForm["ano_extreno"].value;
  const duracion = moviesForm["duracion"].value;
  const genero = moviesForm["genero"].value;
  const categoria = moviesForm["categoria"].value;
  const actor = moviesForm["actor"].value;
  const director = moviesForm["director"].value;



  const url = movieId !== "" ? `/api/movies/${movieId}` : "/api/movies";
  const method = movieId !== "" ? `PUT` : "POST";

  const response = await fetch(url, {
    method: method,
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      titulo: titulo,
      sinopsis: sinopsis,
      url_pelicula: url_pelicula,
      ano_extreno: ano_extreno,
      duracion: duracion,
      genero: genero,
      categoria: categoria,
      actor: actor,
      director: director,

/*       author_id: 2,
      language: "English",
      rating: "8.5", */
    }),
  });
  const data = await response.json();

  if (movieId !== "") {
    rmMovieRow(data.id_pelicula);
  }
  addMovieRow(
    data.id_pelicula,
    data.titulo,
    data.sinopsis,
    data.url_pelicula,
    data.ano_extreno,
    data.duracion,
    data.genero,
    data.categoria,
    data.actor,
    data.director
  );

  moviesForm.reset();
});

window.addEventListener("DOMContentLoaded", async () => {
  const response = await fetch("/api/movies");
  const data = await response.json();
  for (movie of data) {
    addMovieRow(
      data.id_pelicula,
      data.titulo,
      data.sinopsis,
      data.url_pelicula,
      data.ano_extreno,
      data.duracion,
      data.genero,
      data.categoria,
      data.actor,
      data.director
    );
  }
});
