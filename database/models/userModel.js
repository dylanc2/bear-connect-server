const mongoose = require("mongoose");

const Schema = mongoose.Schema;

const userSchema = new Schema(
  {
    name: { type: String, required: true },
    year: { type: String, required: true },
    major: { type: String, required: true },
    classes: { type: String, required: true },
    meetingTimes: { type: [String], required: true },
  },
  {
    timestamps: true, // create timestamp fields
  }
);

const User = mongoose.model("User", userSchema);

module.exports = User;
