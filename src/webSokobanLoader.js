// Configuración
let DB_NAME = "SpaceSokoban";
let STORE_NAME = "snapshots";
let TARGET_LID = "200";
//Valores a modificar:
let NEW_SOLUTION = "RlLruurrdrddlUUUUdddrrrruulululLLrddlluUUdlldddlddrUUUUdddlllluurururRRlddrruU"
let NEW_STEPS_COUNT = 78
let NEW_LEVEL_NAME = "soko 01"


const NEW_DATA = {
  lid: TARGET_LID,
  data: {
  solution: NEW_SOLUTION,
  comparator: NEW_STEPS_COUNT,
  date: 1755730757525,
  uid: 0,
  user: "anonimous",
  lname: NEW_LEVEL_NAME,
  cname: " aenigma",
  cid: 4
  }
};


let request = indexedDB.open(DB_NAME);

request.onsuccess = function(event) {
    let db = event.target.result;
    let transaction = db.transaction(["snapshots"], "readwrite");
    let store = transaction.objectStore("snapshots");

    // Insertar el objeto
    let newRecord = NEW_DATA;

    store.put(newRecord);
    console.log("Registro insertado:", newRecord);
};
