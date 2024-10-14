import { Card, Subtitle, Title } from "@tremor/react";
import { PlaceholderSankey } from "./PlaceholderSankey";

export const CorrelationPlaceholder = () => {
  return (
    <Card className="flex flex-col items-center justify-center gap-y-8 h-full">
      <div className="text-center space-y-3">
        <Title className="text-2xl">No Correlations Yet</Title>
        <Subtitle className="text-gray-400">
          Start building correlation and get all relevant alerts in one
          dedicated place
        </Subtitle>
      </div>
      <PlaceholderSankey className="max-w-full" />
    </Card>
  );
};
