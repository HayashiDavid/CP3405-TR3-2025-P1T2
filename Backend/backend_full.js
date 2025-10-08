// ==============================
// SmartSeats Backend (Single File)
// Sequelize + MySQL
// ==============================

// 1️⃣ Database Configuration
const { Sequelize, DataTypes } = require("sequelize");

const DB = "smartseats";
const USER = "root";
const PASSWORD = "password";
const HOST = "localhost";
const DIALECT = "mysql";

// 2️⃣ Connect to Database
const sequelize = new Sequelize(DB, USER, PASSWORD, {
  host: HOST,
  dialect: DIALECT,
});

const db = {};
db.Sequelize = Sequelize;
db.sequelize = sequelize;

// 3️⃣ Define Models
db.User = sequelize.define("User", {
  name: DataTypes.STRING,
  email: { type: DataTypes.STRING, unique: true },
});

db.Event = sequelize.define("Event", {
  title: DataTypes.STRING,
  date: DataTypes.DATE,
  venue: DataTypes.STRING,
});

db.Seat = sequelize.define("Seat", {
  row: DataTypes.STRING,
  number: DataTypes.INTEGER,
  status: {
    type: DataTypes.ENUM("available", "reserved"),
    defaultValue: "available",
  },
});

db.Reservation = sequelize.define("Reservation", {});

// 4️⃣ Define Associations
db.Event.hasMany(db.Seat);
db.Seat.belongsTo(db.Event);

db.User.hasMany(db.Reservation);
db.Reservation.belongsTo(db.User);

db.Event.hasMany(db.Reservation);
db.Reservation.belongsTo(db.Event);

db.Seat.hasOne(db.Reservation);
db.Reservation.belongsTo(db.Seat);

// 5️⃣ Initialize Database with Sample Data
async function init() {
  try {
    await sequelize.sync({ force: true }); // Drops & recreates tables
    console.log("✅ MySQL DB synced for SmartSeats");

    // Sample inserts
    const user = await db.User.create({
      name: "Alice",
      email: "alice@example.com",
    });

    const event = await db.Event.create({
      title: "Music Fest",
      date: "2025-12-01",
      venue: "Hall A",
    });

    const seat1 = await db.Seat.create({ eventId: event.id, row: "A", number: 1 });
    const seat2 = await db.Seat.create({ eventId: event.id, row: "A", number: 2 });

    await db.Reservation.create({
      userId: user.id,
      eventId: event.id,
      seatId: seat2.id,
    });

    await seat2.update({ status: "reserved" });

    console.log("🎉 Sample reservation created successfully");
  } catch (err) {
    console.error("❌ Error initializing DB:", err);
  }
}

// 6️⃣ Run the Script
init();
