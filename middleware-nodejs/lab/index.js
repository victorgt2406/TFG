const { Client } = require("@opensearch-project/opensearch");


async function main() {
  // Conect to opensearch
  var host = "opensearch-node";
  var protocol = "https";
  var port = 9200;
  var auth = "admin:tfg_openSearch%3FPassword-24"; // For testing only. Don't store credentials in code.

  var client = new Client({
    node: protocol + "://" + auth + "@" + host + ":" + port,
    ssl: {
      rejectUnauthorized: false
    }
  });



  // Creating a index

  var index_name = "books";

  var settings = {
    settings: {
      index: {
        number_of_shards: 4,
        number_of_replicas: 3,
      },
    },
  };

  var response = await client.indices.create({
    index: index_name,
    body: settings,
  });

  console.log("Creating index: ", response)

  // Indexing document


  var document = {
    title: "The Outsider",
    author: "Stephen King",
    year: "2018",
    genre: "Crime fiction",
  };

  var id = "1";

  var response = await client.index({
    id: id,
    index: index_name,
    body: document,
    refresh: true,
  });

  console.log("Indexing document : ", response)

  // Getting document

  var query = {
    query: {
      match: {
        title: {
          query: "The Outsider",
        },
      },
    },
  };

  var response = await client.search({
    index: index_name,
    body: query,
  });

  console.log("Getting document : ", response)
}

main();