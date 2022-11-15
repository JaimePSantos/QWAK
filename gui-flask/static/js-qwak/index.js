const { MongoClient } = require("mongodb");
// Connection URI
const uri =
  "mongodb://localhost:27017/";
// Create a new MongoClient
const client = new MongoClient(uri);

async function run() {
  try {
    await client.connect();
    await client.db("admin").command({ ping: 1 });
    console.log("Connected successfully to server");

    await(listDatabases(client))
    var probDistDB = client.db("flas_db").collection("probDistEntry");
    await findOneListingByName(client,"StaticQWAK-N100-T10");
    // console.log(probDistDB)
    // await createListing(client,
    //     {
    //       0: false,
    //       1: [1,2,3]
    //     }
    //     )
  }
  catch (e) {
    console.error(e);
  }
  finally {
    await client.close();
  }
}

async function listDatabases(client){
    databasesList = await client.db().admin().listDatabases();

    console.log("Databases:");
    databasesList.databases.forEach(db => console.log(` - ${db.name}`));
};

async function createListing(client, newListing){
    const result = await client.db("flas_db").collection("probDistEntry").insertOne(newListing);
    console.log(`New listing created with the following id: ${result.insertedId}`);
}

async function findOneListingByName(client, nameOfListing) {
    const result = await client.db("flas_db").collection("probDistEntry").findOne({ name: nameOfListing });

    if (result) {
        console.log(`Found a listing in the collection with the name '${nameOfListing}':`);
        console.log(result);
    } else {
        console.log(`No listings found with the name '${nameOfListing}'`);
    }
}

async function findListings(client,time, {
    maximumTime = time,
    maximumNumberOfResults = Number.MAX_SAFE_INTEGER
} = {}) {
    const cursor = client.db("flas_db").collection("probDistEntry").find(
                            {
                                walkTime: { $gte: minimumNumberOfBedrooms },
                            }
                            ).sort({ last_review: -1 })
                            .limit(maximumNumberOfResults);

    const results = await cursor.toArray();

    if (results.length > 0) {
        console.log(`Found listing(s) with at least ${minimumNumberOfBedrooms} bedrooms and ${minimumNumberOfBathrooms} bathrooms:`);
        results.forEach((result, i) => {
            date = new Date(result.last_review).toDateString();

            console.log();
            console.log(`${i + 1}. name: ${result.name}`);
            console.log(`   _id: ${result._id}`);
            console.log(`   bedrooms: ${result.bedrooms}`);
            console.log(`   bathrooms: ${result.bathrooms}`);
            console.log(`   most recent review date: ${new Date(result.last_review).toDateString()}`);
        });
    } else {
        console.log(`No listings found with at least ${minimumNumberOfBedrooms} bedrooms and ${minimumNumberOfBathrooms} bathrooms`);
    }
}
run().catch(console.dir);