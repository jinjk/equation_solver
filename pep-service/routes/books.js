var express = require('express');
var router = express.Router();

/* GET users listing. */
router.get('/search', async function (req, res, next) {
        // get req params fileName
    const text = req.query.text;
    console.log(`param text: ${text}`);
    const elsClient = req.app.get('elsClient');
    result = await elsClient.search({
        index: 'pep_books',
        query: {
          match: {
            text: {
                query: text,
                operator: 'and'
            }
          }
        }
      });
    console.log(result);
    return res.send(result);
});

module.exports = router;
