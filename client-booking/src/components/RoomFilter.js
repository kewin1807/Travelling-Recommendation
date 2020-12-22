import React from "react";
import { useContext } from "react";
import { RoomContext } from "../Context";
import Title from "../components/Title";
import { LIST_ID_CITY } from "../constant"



export default function RoomFilter({ rooms }) {
  const context = useContext(RoomContext);
  // console.log(context);

  const {
    handleChange,
    province,
    type_price_hotel,
    type_price_tour
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

  let price_hotels = { "-1": "Tất cả", "0": "Từ 0đ - 400,000 đ", "1": "Từ 400,000đ đến 1,000,000 đ", "2": "Từ 1,000,000đ đến 2,000,000đ", "3": "Từ 2,000,000 trở lên" }
  let price_tours = { "-1": "Tất cả", "0": "Nhỏ hơn 2,000,000 đ", "1": "Từ 2,000,000đ đến 4,000,000 đ", "2": "Từ 4,000,000đ đến 8,000,000đ", "3": "Từ 8,000,000 trở lên" }
  const price_hotels_select = Object.keys(price_hotels).map((item, index) => {
    return (
      <option key={index} value={item}>
        {price_hotels[item]}
      </option>
    );
  });
  const price_tours_select = Object.keys(price_tours).map((item, index) => {
    return (
      <option key={index} value={item}>
        {price_tours[item]}
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
        <div className="form-group">
          <label htmlFor="capacity">Giá tiền mong muốn ở khách sạn</label>
          <select
            name="type_price_hotel"
            id="type_price_hotel"
            onChange={handleChange}
            className="form-control"
            value={type_price_hotel}
          >
            {price_hotels_select}
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="capacity">Giá tiền mong muốn đi tour du lịch</label>
          <select
            name="type_price_tour"
            id="type_price_tour"
            onChange={handleChange}
            className="form-control"
            value={type_price_tour}
          >
            {price_tours_select}
          </select>
        </div>
      </form>
    </section>
  );
}
