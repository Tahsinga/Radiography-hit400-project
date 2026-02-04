const express = require('express');
const router = express.Router();

// Get all users
router.get('/', (req, res) => {
  res.json({ message: 'Get all users' });
});

// Get user by ID
router.get('/:id', (req, res) => {
  res.json({ message: `Get user ${req.params.id}` });
});

// Create user
router.post('/', (req, res) => {
  res.json({ message: 'User created' });
});

// Update user
router.put('/:id', (req, res) => {
  res.json({ message: `User ${req.params.id} updated` });
});

// Delete user
router.delete('/:id', (req, res) => {
  res.json({ message: `User ${req.params.id} deleted` });
});

module.exports = router;
