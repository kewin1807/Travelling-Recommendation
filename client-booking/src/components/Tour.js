import React from "react";
import { Link } from "react-router-dom";
import defaultImg from "../images/room-1.jpeg";
import PropTypes from "prop-types";
export default function Tour({ tour }) {
    const { name, tour_id, image, link, price, rating, number_people_rating, start_date, start_hour, number_available_seat, number_days } = tour;
    const formatMoney = (text) => {
        return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(text)
    }
    return (
        <article className="room">
            <div className="img-container">
                <img src={image || defaultImg} alt="single room" />
                <div className="price-top">
                    <h6>{formatMoney(price)}</h6>
                    <p>trong {number_days} ngày</p>
                </div>
                {/* <Link to={link} className="btn-primary room-link">
            Features
          </Link> */}
                <a className="btn-primary room-link" href={link} target="_blank">Chi tiết</a>
            </div>
            <div style={{ padding: 10 }}>
                <p className="room-info">{name}</p>
                <p> Mã tour: {tour_id} </p>
                <p>Ngày bắt đầu: {start_date} vào lúc {start_hour}</p>
                <p> Số chỗ còn trống: {number_available_seat} </p>
                <p>Đánh giá phục vụ: {rating}/5 trong {number_people_rating} số người đánh giá</p>

            </div>

            {/* <Rate disabled defaultValue={quality_star} /> */}


        </article>
    );
}
