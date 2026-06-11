// ═══════════════════════════════════════════════════════════
//  Je danse en ligne — Apps Script
//  Reçoit les données de GitHub Actions et remplace
//  le contenu de chaque onglet entièrement.
// ═══════════════════════════════════════════════════════════

const ONGLET_SOIREES = "Soirées";
const ONGLET_COURS   = "Cours";

const EN_TETES_SOIREES = [
  "Type","Organisateur","Association","Lieu / Centre","Adresse",
  "Récurrent","Jour(s)","Heure début","Heure fin",
  "Date début","Date fin","Prix","Précisions",
  "URL source","URL association","Saison"
];

const EN_TETES_COURS = [
  "Organisateur","Association","Lieu / Centre","Adresse",
  "Jour(s)","Heure début","Heure fin",
  "Date début","Date fin","Prix","Niveau","Précisions",
  "URL source","URL association","Saison"
];

function doPost(e) {
  try {
    const payload = JSON.parse(e.postData.contents);
    const onglet  = payload.onglet;
    const lignes  = payload.lignes;
    const entetes = onglet === ONGLET_SOIREES ? EN_TETES_SOIREES : EN_TETES_COURS;

    const ss    = SpreadsheetApp.getActiveSpreadsheet();
    let sheet   = ss.getSheetByName(onglet);

    if (!sheet) {
      sheet = ss.insertSheet(onglet);
    }

    sheet.clearContents();
    sheet.getRange(1, 1, 1, entetes.length).setValues([entetes]);
    formaterEntetes(sheet, entetes.length);

    if (lignes.length > 0) {
      sheet.getRange(2, 1, lignes.length, entetes.length).setValues(lignes);
    }

    return reponse({ succes: true, onglet: onglet, lignes: lignes.length });
  } catch(err) {
    return reponse({ succes: false, erreur: err.toString() });
  }
}

function doGet(e) {
  return reponse({ statut: "Je danse en ligne — API active" });
}

function formaterEntetes(sheet, nbCols) {
  const range = sheet.getRange(1, 1, 1, nbCols);
  range.setBackground("#2C5F8A");
  range.setFontColor("#FFFFFF");
  range.setFontWeight("bold");
  range.setFontFamily("Arial");
  sheet.setFrozenRows(1);
  sheet.setRowHeight(1, 36);
}

function reponse(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
