const router = require("express").Router();
let User = require("../models/userModel"); // mongoose model

// CREATE
router.route("/add").post((req, res) => {
  const _id = req.body._id
  const name = req.body.name;
  const year = req.body.year;
  const major = req.body.major;
  const selectedClass = req.body.selectedClass;
  const studyTimes = req.body.studyTimes;
  const meetingTimes = req.body.meetingTimes;
  const studyStyle = req.body.studyStyle;

  const newUser = new User({
    _id,
    name,
    year,
    major,
    selectedClass,
    studyTimes,
    meetingTimes,
    studyStyle
  });

  newUser.save()
    .then(() => res.json("User added!"))
    .catch((err) => res.status(400).json("Error: " + err));
});

// READ
router.route("/").get((req, res) => {
  User.find()
    .then((users) => res.json(users))
    .catch((err) => res.status(400).json("Error: " + err));
});

router.route("/:id").get((req, res) => {
  User.findById(req.params.id)
    .then((user) => res.json(user))
    .catch((err) => res.status(400).json("Error: " + err));
});

// UPDATE
router.route("/:id").put((req, res) => {
  User.findById(req.params.id)
    .then((user) => {
      user.name = req.body.name || user.name;
      user.year = req.body.year || user.year;
      user.selectedClass = req.body.selectedClass || user.selectedClass;
      user.major = req.body.major || user.major;
      user.meetingTimes = req.body.meetingTimes || user.meetingTimes;
      user.studyTimes = req.body.studyTimes || user.studyTimes;
      user.studyStyle = req.body.studyStyle || user.studyStyle;

      user.save()
        .then(() => res.json("User updated!"))
        .catch((err) => res.status(400).json("Error: " + err));
    })
    .catch((err) => res.status(400).json("Error: " + err));
});

// DELETE
router.route("/:id").delete((req, res) => {
  User.findByIdAndDelete(req.params.id)
    .then(() => res.json("User deleted."))
    .catch((err) => res.status(400).json("Error: " + err));
});

module.exports = router;
