
import React from "react";
import Tour from "./Tour";
export default function TourList({ tours }) {
    if (tours.length === 0) {
        return (
            <div className="empty-search">
                <h6>Các tour du lịch</h6>
                <h3>Không tìm được kết quả phù hợp</h3>
            </div>
        );
    }
    return (
        // <section className="roomslist">
        //     <div className="roomslist-center">
        //         {tours.map(item => {
        //             return <Room key={item.id} room={item} />;
        //         })}
        //     </div>
        // </section>
        <div>
            <div className="empty-search">
                <h6>Các tour du lịch</h6>
            </div>
            <section className="roomslist">
                <div className="roomslist-center">
                    {tours.map(item => {
                        return <Tour key={item.id} tour={item} />;
                    })}
                </div>
            </section>
        </div>

    );
}