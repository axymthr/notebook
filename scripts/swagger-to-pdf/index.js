const fs = require('fs');
const pdf = require('pdfjs')

async function parseSwagger(doc, sjson) {
	var cell = doc.cell({ paddingBottom: 0.5*pdf.cm })
	cell.text(`${sjson.info.title}`, { fontSize: 16, color: 0xf8cd3f })
	cell.text(`${sjson.info.description}`, { fontSize: 10 })

	doc.pipe(fs.createWriteStream('output.pdf'))
	await doc.end()
}

let sjson = null;
fs.promises.readFile("./swagger.json").then(file => {
	sjson = JSON.parse(file)
	const doc = new pdf.Document({
		font: require('pdfjs/font/Helvetica'),
		padding: 20,
		properties: {
			title: 'Sample output'
		}
	})
	parseSwagger(doc,sjson)
}).catch(err => {
	console.error('Error reading swagger json', error)
})
// create pdfjs doc

