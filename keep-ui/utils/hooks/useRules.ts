import { useSession } from "next-auth/react";
import useSWR, { SWRConfiguration } from "swr";
import { getApiURL } from "utils/apiUrl";
import { fetcher } from "utils/fetcher";

export type Rule = {
  id: string;
  name: string;
  item_description: string | null;
  group_description: string | null;
  grouping_criteria: string[];
  definition_cel: string;
  definition: { sql: string; params: {} };
  timeframe: number;
  timeunit: "minutes" | "seconds" | "hours" | "days";
  created_by: string;
  creation_time: string;
  tenant_id: string;
  updated_by: string | null;
  update_time: string | null;
  require_approve: boolean;
  distribution: { [group: string]: { [timestamp: string]: number } };
  incidents: number
};

export const useRules = (options?: SWRConfiguration) => {
  const apiUrl = getApiURL();
  const { data: session } = useSession();

  return useSWR<Rule[]>(
    () => (session ? `${apiUrl}/rules` : null),
    async (url) => fetcher(url, session?.accessToken),
    options
  );
};

export const useAIGeneratedRules = (options?: SWRConfiguration) => {
  const apiUrl = getApiURL();
  const { data: session } = useSession();

  const { data, error, isLoading, mutate } = useSWR(
    () => (session ? `${apiUrl}/rules/gen_rules` : null),
    async (url) => {
      const response = await fetcher(url, session?.accessToken);
      return JSON.parse(JSON.stringify(response)); // Ensure we return a JSON object
    },
    {
      ...options,
      revalidateOnFocus: false,
      revalidateOnReconnect: false,
    }
  );

  const mutateAIGeneratedRules = async () => {
    // Set data to undefined to trigger loading state
    await mutate(undefined, { revalidate: true });
  };

  return { data, error, isLoading, mutateAIGeneratedRules };
};
