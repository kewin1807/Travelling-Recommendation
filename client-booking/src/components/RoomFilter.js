import React from "react";
import { useContext } from "react";
import { RoomContext } from "../Context";
import Title from "../components/Title";
import { LIST_ID_CITY } from "../constant"
//get unique values
const getUnique = (items, value) => {
  return [...new Set(items.map(item => item[value]))];
};

export default function RoomFilter({ rooms }) {
  const context = useContext(RoomContext);
  // console.log(context);

  const {
    handleChange,
    province,
  } = context;
  //map to jsx
  const cities = { ...{ "Chọn điểm đến": "Chọn điểm đến" }, ...LIST_ID_CITY }
  const provinces = Object.keys(cities).map((item, index) => {
    return (
      <option value={item} key={index}>
        {cities[item]}
      </option>
    );
  });

  let people = getUnique(rooms, "capacity");
  people = people.map((item, index) => {
    return (
      <option key={index} value={item}>
        {item}
      </option>
    );
  });

  return (
    <section className="filter-container">
      <Title title="search rooms" />
      <form className="filter-form">
        {/* select province */}
        <div className="form-group">
          <label htmlFor="type">Điểm đến</label>
          <select
            name="province"
            id="province"
            value={province}
            className="form-control"
            onChange={handleChange}
          >
            {provinces}
          </select>
        </div>
      </form>
    </section>
  );
}
