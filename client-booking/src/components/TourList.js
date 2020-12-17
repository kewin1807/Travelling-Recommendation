
import React from "react";
import Room from "./Room";
export default function RoomList({ tours }) {
    if (tours.length === 0) {
        return (
            <div className="empty-search">
                <h3>unfortunately no rooms matched your search parameters</h3>
            </div>
        );
    }
    return (
        <section className="roomslist">
            <div className="roomslist-center">
                {tours.map(item => {
                    return <Room key={item.id} room={item} />;
                })}
            </div>
        </section>
    );
}