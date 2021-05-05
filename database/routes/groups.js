const router = require("express").Router();
const axios = require("axios");
var ObjectId = require("mongodb").ObjectID;
let Group = require("../models/groupModel");
let User = require("../models/userModel");

// CREATE
router.route("/add").post((req, res) => {
  const members = req.body.members;
  const open = req.body.open;
  const sizeLimit = Number(req.body.sizeLimit);
  const className = req.body.className;

  function getDiscord() {
    return axios
      .post("http://host.docker.internal:5003/create_channel") //depends on docker config
      .then((response) => {
        this.response = response.data;
        return this.response.channel_invite;
      });
  }

  getDiscord().then((data) => {
    discordLink = data;
    console.log(discordLink);

    const newGroup = new Group({
      members,
      open,
      sizeLimit,
      className,
      discordLink,
    });

    newGroup
      .save()
      .then(() => res.json("Group added!"))
      .catch((err) => res.status(400).json("Error: " + err));
  });
});

router.route("/addWithoutLink").post((req, res) => {
  const members = req.body.members;
  const open = req.body.open;
  const sizeLimit = Number(req.body.sizeLimit);
  const className = req.body.className;
  const discordLink = req.body.discordLink;

  const newGroup = new Group({
    members,
    open,
    sizeLimit,
    className,
    discordLink
  });

  newGroup
    .save()
    .then(() => res.json("Group added!"))
    .catch((err) => res.status(400).json("Error: " + err));
});

// READ
router.route("/").get((req, res) => {
  Group.find()
    .then((groups) => res.json(groups))
    .catch((err) => res.status(400).json("Error: " + err));
});

router.route("/:id").get((req, res) => {
  Group.findById(req.params.id)
    .then((group) => res.json(group))
    .catch((err) => res.status(400).json("Error: " + err));
});

// UPDATE
router.route("/:id").put((req, res) => {
  Group.findById(req.params.id)
    .then((group) => {
      group.members = req.body.members;
      group.open = req.body.open;
      group.sizeLimit = Number(req.body.sizeLimit);
      group.className = req.body.className;

      group
        .save()
        .then(() => res.json("Group updated!"))
        .catch((err) => res.status(400).json("Error: " + err));
    })
    .catch((err) => res.status(400).json("Error: " + err));
});

// Add user to group
router.route("/addUser/:id").put((req, res) => {
  Group.findById(req.params.id)
    .then((group) => {
      if (group.members.length == group.sizeLimit) {
        res.json("Sorry, this group is full.")
      } else {
        if (group.open) {
          group.members.push(req.body.user);
        }
        console.log(group.members.length);
        if (group.members.length == group.sizeLimit) {
          group.open = false;
        }
        group
        .save()
        .then(() => res.json({discordLink: group.discordLink}))
        .catch((err) => res.status(400).json("Error: " + err));
      }
    })
    .catch((err) => res.status(400).json("Error: " + err));
});

// DELETE
router.route("/:id").delete((req, res) => {
  Group.findByIdAndDelete(req.params.id)
    .then(() => res.json("Group deleted."))
    .catch((err) => res.status(400).json("Error: " + err));
});

// Best groups
router.route("/bestGroups/:id").get(async (req, res) => {
  const user = await User.findById(req.params.id);
  const groups = await Group.find({ className: user.selectedClass });

  let groupData = [];
  groups.forEach((group) => {
    groupProps = {
      _id: null,
      names: [],
      years: [],
      majors: [],
      meetingTimes: [],
      studyTimes: [],
      studyStyles: [],
    };
    group.members.forEach((member) => {
      groupProps["names"].push(member.name);
      groupProps["years"].push(member.year);
      groupProps["majors"].push(member.major);
      groupProps["meetingTimes"].push(member.meetingTimes);
      groupProps["studyTimes"].push(member.studyTimes);
      groupProps["studyStyles"].push(member.studyStyle);
    });
    groupProps["_id"] = group._id;
    groupData.push(groupProps);
    groupProps = {
      years: [],
      majors: [],
      meetingTimes: [],
      studyTimes: [],
      studyStyles: [],
    };
  });

  let ranks = {};
  let w = { 1: 3, 2: 1, 3: 1, 4: 1, 5: 1 };
  let yearToInt = {
    freshman: 1,
    sophomore: 2,
    junior: 3,
    senior: 4,
    "master's": 5,
    phd: 6,
  };
  groupData.forEach((group) => {
    let [
      yearFeature,
      majorFeature,
      meetingTimesFeature,
      studyTimesFeature,
      studyStyleFeature,
    ] = Array(5).fill(0);

    yearNums = group.years.map((x) => yearToInt[x]);
    let avgYear = Object.values(yearNums).reduce((a, b) => a + b) / 2;
    // console.log(yearNums);
    // console.log(avgYear);
    // console.log(yearToInt[user.year]);

    if (Math.abs(avgYear - yearToInt[user.year]) <= 1) {
      yearFeature = 1;
    }
    if (group.majors.includes(user.major)) {
      majorFeature = 1;
    }
    if (group.meetingTimes.includes(user.meetingTimes)) {
      meetingTimesFeature = 1;
    }
    if (group.studyTimes.includes(user.studyTimes)) {
      studyTimesFeature = 1;
    }
    if (group.studyStyles.includes(user.studyStyle)) {
      studyStyleFeature = 1;
    }

    let score =
      w[1] * yearFeature +
      w[2] * majorFeature +
      w[3] * meetingTimesFeature +
      w[4] * studyTimesFeature +
      w[5] * studyStyleFeature;
    ranks[group._id] = score;
  });

  rankedGroupKeys = Object.keys(ranks).sort().reverse();

  bestGroups = [];
  rankedGroupKeys.forEach((id) => {
    groups.forEach((group) => {
      if (group._id == id) {
        bestGroups.push(group);
      }
    });
  });

  res.json(bestGroups);
});

module.exports = router;
