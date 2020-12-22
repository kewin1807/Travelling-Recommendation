import React from "react";
import { Link } from "react-router-dom";
import defaultImg from "../images/room-1.jpeg";
import PropTypes from "prop-types";
import { Card, Rate, Row, Col } from "antd";

export default function Room({ room }) {
  // console.log(room);
  const { address, description, image, link, price, quality, rating, number_people_rating, name, distance_calc } = room;
  const formatMoney = (text) => {
    return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(text)
  }
  return (
    <article className="room">
      <div className="img-container">
        <img src={image || defaultImg} alt="single room" />
        <div className="price-top">
          <h6>{formatMoney(price)}</h6>
          <p>per night</p>
        </div>
        {/* <Link to={link} className="btn-primary room-link">
          Features
        </Link> */}
        <a className="btn-primary room-link" href={link} target="_blank">Chi tiết</a>
      </div>
      <div style={{ padding: 5 }}>
        <p className="room-info">{name}</p>
        <h6>Địa chỉ: {address}</h6>
        <h6>Mô tả: {description}</h6>
        <p>Khoảng cách đến trung tâm thành phố: {distance_calc ? `${distance_calc} km` : "Không xác định"} </p>
        <p>Chất lượng khách sạn : {quality} sao</p>
        <p>Đánh giá phục vụ: {rating} / {number_people_rating} số người đánh giá</p>
      </div>

      {/* <Rate disabled defaultValue={quality_star} /> */}


    </article>
  );
}

Room.propTypes = {
  room: PropTypes.shape({
    name: PropTypes.string.isRequired,
    slug: PropTypes.string.isRequired,
    images: PropTypes.arrayOf(PropTypes.string).isRequired,
    price: PropTypes.number.isRequired
  })
};
