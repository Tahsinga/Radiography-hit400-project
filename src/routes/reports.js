const express = require('express');
const router = express.Router();

// Get all reports
router.get('/', (req, res) => {
  res.json({ message: 'Get all reports' });
});

// Get report by ID
router.get('/:id', (req, res) => {
  res.json({ message: `Get report ${req.params.id}` });
});

// Create report
router.post('/', (req, res) => {
  res.json({ message: 'Report created' });
});

// Update report
router.put('/:id', (req, res) => {
  res.json({ message: `Report ${req.params.id} updated` });
});

// Delete report
router.delete('/:id', (req, res) => {
  res.json({ message: `Report ${req.params.id} deleted` });
});

module.exports = router;
