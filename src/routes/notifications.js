const express = require('express');
const router = express.Router();

// Get all notifications
router.get('/', (req, res) => {
  res.json({ message: 'Get all notifications' });
});

// Get notification by ID
router.get('/:id', (req, res) => {
  res.json({ message: `Get notification ${req.params.id}` });
});

// Send notification
router.post('/', (req, res) => {
  res.json({ message: 'Notification sent' });
});

// Mark as read
router.put('/:id/read', (req, res) => {
  res.json({ message: `Notification ${req.params.id} marked as read` });
});

module.exports = router;
