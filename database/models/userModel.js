const mongoose = require("mongoose");

const Schema = mongoose.Schema;

const userSchema = new Schema(
  {
    _id: { type: String, required: true },
    name: { type: String, required: true },
    year: { type: String, required: true },
    major: { type: String, required: true },
    selectedClass: { type: String, required: true },
    studyTimes: { type: String, required: true },
    meetingTimes: { type: String, required: true },
    studyStyle: { type: String, required: true }
  },
  {
    timestamps: true, // create timestamp fields
  }
);

const User = mongoose.model("User", userSchema);

module.exports = User;
