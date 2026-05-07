import { cn } from "@/lib/utils";

function Skeleton({
	className,
	...props
}: React.HTMLAttributes<HTMLDivElement>) {
	return (
		<div
			className={cn(
				"animate-gradient-wave rounded-md bg-gradient-to-r from-[#707070] via-[#0f4beb] via-[#0f4beb] to-[#ff2305]",
				className,
			)}
			{...props}
		/>
	);
}

export { Skeleton };
