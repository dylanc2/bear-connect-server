const mongoose = require("mongoose");

const Schema = mongoose.Schema;

const groupSchema = new Schema(
  {
    open: { type: Boolean, required: true },
    sizeLimit: { type: Number, required: true },
    className: { type: String, required: true },
    members: { type: [{_id: String, name: String, year: String, major: String, selectedClass: String, meetingTimes: String, studyTimes: String, studyStyle: String}], required: true },
    discordLink: {type: String, required: true},
    // majors: { type: [String], required: true },
    // meetingTimes: { type: [String], required: true },
    // studyTimes: { type: [String], required: true },
    // studyStyles: { type: [String], required: true },
  },
  {
    timestamps: true,
  }
);

const Group = mongoose.model("Group", groupSchema);

module.exports = Group;
