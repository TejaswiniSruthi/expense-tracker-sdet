const mongoose = require('mongoose');

const expenseSchema = new mongoose.Schema(
  {
    amount: {
      type: Number,
      required: [true, 'amount is required'],
      min: [0.01, 'amount must be greater than 0'],
    },
    category: {
      type: String,
      required: [true, 'category is required'],
      enum: ['Food', 'Travel', 'Shopping', 'Bills', 'Entertainment', 'Health', 'Other'],
    },
    description: {
      type: String,
      trim: true,
      maxlength: 200,
    },
    paymentMethod: {
      type: String,
      enum: ['cash', 'card', 'upi', 'netbanking'],
      default: 'cash',
    },
    date: {
      type: Date,
      default: Date.now,
    },
  },
  { timestamps: true }
);

module.exports = mongoose.model('Expense', expenseSchema);