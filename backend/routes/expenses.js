const express = require('express');
const Expense = require('../models/Expense');

const router = express.Router();

// POST /api/expenses — create
router.post('/', async (req, res) => {
  try {
    const expense = await Expense.create(req.body);
    res.status(201).json(expense);
  } catch (err) {
    if (err.name === 'ValidationError') {
      return res.status(400).json({ error: err.message });
    }
    res.status(500).json({ error: 'Internal server error' });
  }
});

// GET /api/expenses — list with optional filters
// ?category=Food  &from=2026-07-01  &to=2026-07-31
router.get('/', async (req, res) => {
  try {
    const filter = {};
    if (req.query.category) filter.category = req.query.category;
    if (req.query.from || req.query.to) {
      filter.date = {};
      if (req.query.from) filter.date.$gte = new Date(req.query.from);
      if (req.query.to) filter.date.$lte = new Date(req.query.to);
    }
    const expenses = await Expense.find(filter).sort({ date: -1 });
    res.status(200).json(expenses);
  } catch (err) {
    res.status(500).json({ error: 'Internal server error' });
  }
});

// GET /api/expenses/summary — totals by category
// NOTE: must be defined BEFORE /:id or "summary" gets treated as an id
router.get('/summary', async (req, res) => {
  try {
    const summary = await Expense.aggregate([
      {
        $group: {
          _id: '$category',
          total: { $sum: '$amount' },
          count: { $sum: 1 },
        },
      },
      { $sort: { total: -1 } },
      {
        $project: { _id: 0, category: '$_id', total: 1, count: 1 },
      },
    ]);
    res.status(200).json(summary);
  } catch (err) {
    res.status(500).json({ error: 'Internal server error' });
  }
});

// GET /api/expenses/:id — single expense
router.get('/:id', async (req, res) => {
  try {
    const expense = await Expense.findById(req.params.id);
    if (!expense) return res.status(404).json({ error: 'Expense not found' });
    res.status(200).json(expense);
  } catch (err) {
    if (err.name === 'CastError') {
      return res.status(400).json({ error: 'Invalid expense id' });
    }
    res.status(500).json({ error: 'Internal server error' });
  }
});

// PUT /api/expenses/:id — update
router.put('/:id', async (req, res) => {
  try {
    const expense = await Expense.findByIdAndUpdate(req.params.id, req.body, {
      new: true,           // return the updated document
      runValidators: true, // apply schema validation on update too
    });
    if (!expense) return res.status(404).json({ error: 'Expense not found' });
    res.status(200).json(expense);
  } catch (err) {
    if (err.name === 'ValidationError') {
      return res.status(400).json({ error: err.message });
    }
    if (err.name === 'CastError') {
      return res.status(400).json({ error: 'Invalid expense id' });
    }
    res.status(500).json({ error: 'Internal server error' });
  }
});

// DELETE /api/expenses/:id — delete
router.delete('/:id', async (req, res) => {
  try {
    const expense = await Expense.findByIdAndDelete(req.params.id);
    if (!expense) return res.status(404).json({ error: 'Expense not found' });
    res.status(204).send();
  } catch (err) {
    if (err.name === 'CastError') {
      return res.status(400).json({ error: 'Invalid expense id' });
    }
    res.status(500).json({ error: 'Internal server error' });
  }
});

module.exports = router;