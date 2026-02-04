const express = require('express');
const router = express.Router();

// Get all appointments
router.get('/', (req, res) => {
  res.json({ message: 'Get all appointments' });
});

// Get appointment by ID
router.get('/:id', (req, res) => {
  res.json({ message: `Get appointment ${req.params.id}` });
});

// Create appointment
router.post('/', (req, res) => {
  res.json({ message: 'Appointment created' });
});

// Update appointment
router.put('/:id', (req, res) => {
  res.json({ message: `Appointment ${req.params.id} updated` });
});

// Delete appointment
router.delete('/:id', (req, res) => {
  res.json({ message: `Appointment ${req.params.id} deleted` });
});

module.exports = router;
