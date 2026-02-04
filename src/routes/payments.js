const express = require('express');
const router = express.Router();

// Get all payments
router.get('/', (req, res) => {
  res.json({ message: 'Get all payments' });
});

// Get payment by ID
router.get('/:id', (req, res) => {
  res.json({ message: `Get payment ${req.params.id}` });
});

// Process payment
router.post('/', (req, res) => {
  res.json({ message: 'Payment processed' });
});

// Get payment status
router.get('/:id/status', (req, res) => {
  res.json({ message: `Get payment ${req.params.id} status` });
});

module.exports = router;
