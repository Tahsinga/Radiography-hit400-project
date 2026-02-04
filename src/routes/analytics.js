const express = require('express');
const router = express.Router();

// Get analytics dashboard
router.get('/', (req, res) => {
  res.json({ message: 'Get analytics data' });
});

// Get specific metric
router.get('/:metric', (req, res) => {
  res.json({ message: `Get ${req.params.metric} analytics` });
});

module.exports = router;
