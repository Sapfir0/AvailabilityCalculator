export const IsochroneSettings = () => {
    return (
        <div className="absolute fl my24 mx24 py24 px24 bg-gray-faint round">
            <form id="params">
                <h4 className="txt-m txt-bold mb6">Choose a travel mode:</h4>
                <div className="mb12 mr12 toggle-group align-center">
                    <label className="toggle-container">
                        <input name="profile" type="radio" value="walking" checked />
                        <div className="toggle toggle--active-null toggle--null">Walking</div>
                    </label>
                    <label className="toggle-container">
                        <input name="profile" type="radio" value="cycling" />
                        <div className="toggle toggle--active-null toggle--null">Cycling</div>
                    </label>
                    <label className="toggle-container">
                        <input name="profile" type="radio" value="driving" />
                        <div className="toggle toggle--active-null toggle--null">Driving</div>
                    </label>
                </div>
                <h4 className="txt-m txt-bold mb6">Choose a maximum duration:</h4>
                <div className="mb12 mr12 toggle-group align-center">
                    <label className="toggle-container">
                        <input name="duration" type="radio" value="10" checked />
                        <div className="toggle toggle--active-null toggle--null">10 min</div>
                    </label>
                    <label className="toggle-container">
                        <input name="duration" type="radio" value="20" />
                        <div className="toggle toggle--active-null toggle--null">20 min</div>
                    </label>
                    <label className="toggle-container">
                        <input name="duration" type="radio" value="30" />
                        <div className="toggle toggle--active-null toggle--null">30 min</div>
                    </label>
                </div>
            </form>
        </div>
    );
};
