const router = require("express").Router();
let Group = require("../models/groupModel");

// CREATE
router.route("/add").post((req, res) => {
  const members = req.body.members;
  const open = req.body.open;
  const sizeLimit = Number(req.body.sizeLimit);
  const className = req.body.className;

  const newGroup = new Group({
    members,
    open,
    sizeLimit,
    className,
  });

  newGroup.save()
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
      group.members = req.body.members || group.members;
      group.open = req.body.open || group.open;
      group.sizeLimit = Number(req.body.sizeLimit) || group.sizeLimit;
      group.className = req.body.className || group.className;

      group.save()
        .then(() => res.json("Group updated!"))
        .catch((err) => res.status(400).json("Error: " + err));
    })
    .catch((err) => res.status(400).json("Error: " + err));
});

// DELETE
router.route("/:id").delete((req, res) => {
  Group.findByIdAndDelete(req.params.id)
    .then(() => res.json("Group deleted."))
    .catch((err) => res.status(400).json("Error: " + err));
});

module.exports = router;
