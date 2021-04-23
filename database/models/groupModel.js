const mongoose = require("mongoose");

const Schema = mongoose.Schema;

const groupSchema = new Schema(
  {
    members: { type: [String], required: true },
    open: { type: Boolean, required: true },
    sizeLimit: { type: Number, required: true },
    className: { type: String, required: true },
  },
  {
    timestamps: true,
  }
);

const Group = mongoose.model("Group", groupSchema);

module.exports = Group;
