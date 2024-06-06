var express = require('express');
var router = express.Router();

/* GET users listing. */
router.get('/search', async function (req, res, next) {
  // get req params fileName
  const text = req.query.text;
  console.log(`param text: ${text}`);
  try {
    const elsClient = req.app.get('elsClient');
    result = await elsClient.search({
      index: 'pep_books',
      sort: ['page'],
      query: {
        match: {
          text: {
            query: text,
            operator: 'and'
          }
        }
      }
    });
    console.log(result.hits);
    res.send(result.hits.hits);
  }
  catch (e) {
    console.log(e);
    res.status(500).send('cannot connect to elasticsearch');
  };
});

function res2doc(item) {

}

module.exports = router;
