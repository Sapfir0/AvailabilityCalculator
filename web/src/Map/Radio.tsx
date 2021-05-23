import { observer } from "mobx-react";

export type RadioProps = {
    value: string;
    defaultValue: string;
    onChange: (val: string) => void;
};

export const Radio = observer(({ value, defaultValue, onChange }: RadioProps) => {    
    return <label className="toggle-container">
        <input
            name={value}
            type="radio"
            value={value}
            checked={defaultValue === value}
            onChange={(e) => onChange(defaultValue)}
        />
        <div className="toggle toggle--active-null toggle--null">{defaultValue}</div>
    </label>
});
