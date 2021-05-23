import { observer } from 'mobx-react';
import { TYPES } from '../inversify/types';
import { useInject } from '../services/hooks';
import { Bufferization, TravelMode } from '../typing';
import { MapStore } from './MapStore';
import { Radio } from './Radio';

export const IsochroneSettings = observer(() => {
    const { setMaxDuration, setTravelMode, maxDuration, travelMode, bufferization, setBufferizationMode } = useInject<MapStore>(TYPES.MapStore);

    return (
        <div className="absolute fl my24 mx24 py24 px24 bg-gray-faint round">
            <form id="params">
                <h4 className="txt-m txt-bold mb6">Choose a travel mode:</h4>
                <div className="mb12 mr12 toggle-group align-center">
                    <Radio value={travelMode} defaultValue={TravelMode[TravelMode.walking]} onChange={setTravelMode} />
                    <Radio value={travelMode} defaultValue={TravelMode[TravelMode.cycling]} onChange={setTravelMode} />
                    <Radio value={travelMode} defaultValue={TravelMode[TravelMode.driving]} onChange={setTravelMode} />
                </div>
                <h4 className="txt-m txt-bold mb6">Choose a maximum duration:</h4>
                <div className="mb12 mr12 toggle-group align-center">
                    <Radio value={maxDuration} defaultValue={'10'} onChange={setMaxDuration} />
                    <Radio value={maxDuration} defaultValue={'20'} onChange={setMaxDuration} />
                    <Radio value={maxDuration} defaultValue={'30'} onChange={setMaxDuration} />
                </div>
                <h4 className="txt-m txt-bold mb6">Choose a bufferization method:</h4>
                <div className="mb12 mr12 toggle-group align-center">
                    <Radio value={bufferization} defaultValue={Bufferization[Bufferization.byAir]} onChange={setBufferizationMode} />
                    <Radio value={bufferization} defaultValue={Bufferization[Bufferization.isochrones]} onChange={setBufferizationMode} />
                </div>
            </form>
        </div>
    );
});
