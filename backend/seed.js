require('dotenv').config();
const mongoose = require('mongoose');
const Expense = require('./models/Expense');

const sampleExpenses = [
  { amount: 250, category: 'Food', description: 'Lunch at office', paymentMethod: 'upi' },
  { amount: 1200, category: 'Travel', description: 'Cab to airport', paymentMethod: 'card' },
  { amount: 3500, category: 'Shopping', description: 'Headphones', paymentMethod: 'card' },
  { amount: 899, category: 'Bills', description: 'Electricity bill', paymentMethod: 'netbanking' },
  { amount: 450, category: 'Entertainment', description: 'Movie tickets', paymentMethod: 'upi' },
  { amount: 600, category: 'Health', description: 'Pharmacy', paymentMethod: 'cash' },
  { amount: 150, category: 'Food', description: 'Coffee and snacks', paymentMethod: 'cash' },
  { amount: 2000, category: 'Travel', description: 'Train tickets', paymentMethod: 'netbanking' },
  { amount: 320, category: 'Food', description: 'Groceries', paymentMethod: 'upi' },
  { amount: 999, category: 'Entertainment', description: 'Annual streaming subscription', paymentMethod: 'card' },
];

async function seed() {
  try {
    await mongoose.connect(process.env.MONGO_URI);
    await Expense.deleteMany({});
    const inserted = await Expense.insertMany(sampleExpenses);
    console.log(`Seeded ${inserted.length} expenses`);
  } catch (err) {
    console.error('Seed failed:', err.message);
    process.exitCode = 1;
  } finally {
    await mongoose.disconnect();
  }
}

seed();