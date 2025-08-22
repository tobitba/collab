// Configuración
let DB_NAME = "SpaceSokoban";
let STORE_NAME = "snapshots";
let TARGET_LID = "200";
//Valores a modificar:
let NEW_SOLUTION = "RlLruurrdrddlUUUUdddrrrruulululLLrddlluUUdlldddlddrUUUUdddlllluurururRRlddrruU"
let NEW_STEPS_COUNT = 78
let NEW_LEVEL_NAME = "soko 01"


const NEW_DATA = {
  solution: NEW_SOLUTION,
  comparator: NEW_STEPS_COUNT,
  date: 1755730757525,
  uid: 0,
  user: "anonimous",
  lname: NEW_LEVEL_NAME,
  cname: " aenigma",
  cid: 4
};


let request = indexedDB.open(DB_NAME);

request.onsuccess = function(event) {
    let db = event.target.result;
    let transaction = db.transaction([STORE_NAME], "readwrite");
    let store = transaction.objectStore(STORE_NAME);

    let cursorRequest = store.openCursor();
    cursorRequest.onsuccess = function(event) {
        let cursor = event.target.result;
        if(cursor) {
            if(cursor.value.lid === TARGET_LID) {
                let record = cursor.value;
                console.log("Antes:", record);

                record.data = NEW_DATA;

                cursor.update(record);
                console.log("Modificado:", record);
            }
            cursor.continue();
        } else {
            console.log("Proceso terminado, registro con lid", TARGET_LID, "modificado si existía.");
        }
    };
};

request.onerror = function(event) {
    console.error("Error al abrir la DB:", event);
};
