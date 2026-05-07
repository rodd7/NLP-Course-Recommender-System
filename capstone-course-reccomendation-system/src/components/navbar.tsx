"use client";

import * as React from "react";
import Link from "next/link";
import Image from "next/image";

import blue_uts_logo from "../../public/uts_blue_logo.jpg";

import { cn } from "@/lib/utils";

import {
	NavigationMenu,
	NavigationMenuContent,
	NavigationMenuItem,
	NavigationMenuLink,
	NavigationMenuList,
	NavigationMenuTrigger,
	navigationMenuTriggerStyle,
} from "@/components/ui/navigation-menu";

const components: { title: string; href: string; description: string }[] = [
	{
		title: "Alert Dialog",
		href: "/docs/primitives/alert-dialog",
		description:
			"A modal dialog that interrupts the user with important content and expects a response.",
	},
	{
		title: "Hover Card",
		href: "/docs/primitives/hover-card",
		description:
			"For sighted users to preview content available behind a link.",
	},
	{
		title: "Progress",
		href: "/docs/primitives/progress",
		description:
			"Displays an indicator showing the completion progress of a task, typically displayed as a progress bar.",
	},
	{
		title: "Scroll-area",
		href: "/docs/primitives/scroll-area",
		description: "Visually or semantically separates content.",
	},
	{
		title: "Tabs",
		href: "/docs/primitives/tabs",
		description:
			"A set of layered sections of content—known as tab panels—that are displayed one at a time.",
	},
	{
		title: "Tooltip",
		href: "/docs/primitives/tooltip",
		description:
			"A popup that displays information related to an element when the element receives keyboard focus or the mouse hovers over it.",
	},
];

export function Navbar() {
	return (
		<div className="flex flex-row bg-navbar py-3">
			<div className="basis-1/5"></div>

			<div className="basis-3/5 flex">
				<Link className="flex items-center gap-2" href="/">
					<Image
						src="/uts_logo_white.svg"
						alt="UTS Logo"
						width={85}
						height={50}
					/>
				</Link>
				<div className="flex-grow flex justify-end">
					<NavigationMenu>
						<NavigationMenuList>
							<NavigationMenuItem>
								<NavigationMenuTrigger>
									University Services
								</NavigationMenuTrigger>
								<NavigationMenuContent>
									<ul className="grid gap-3 p-6 md:w-[400px] lg:w-[500px] lg:grid-cols-[.75fr_1fr]">
										<li className="row-span-3">
											<NavigationMenuLink asChild>
												<a
													className="flex h-full w-full select-none flex-col justify-end rounded-md text-sm bg-gradient-to-b from-muted/50 to-muted p-6 no-underline outline-none focus:shadow-md"
													href="https://www.uts.edu.au/"
												>
													<Image
														src={blue_uts_logo}
														alt="Blue UTS Logo"
														width={60}
														height={60}
														className="rounded mb-3"
													/>
													Study with UTS, or undergo Research Programs and
													Partnerships
												</a>
											</NavigationMenuLink>
										</li>
										<ListItem
											href="https://www.uts.edu.au/current-students/mytimetable"
											title="myTimetable"
										>
											myTimetable is the system used for selecting your classes
											after you have enrolled into your subjects via My Student
											Admin.
										</ListItem>
										<ListItem
											href="https://www.handbook.uts.edu.au/dates_academic.html"
											title="Academic Dates"
											className=""
										>
											Stay on top of important events like term start and end
											dates, enrollment deadlines, exam periods, and breaks.
										</ListItem>
										<ListItem
											href="https://www.lib.uts.edu.au/"
											title="UTS Library"
										>
											Access Library resources, services, or book workshops and
											Library spaces.
										</ListItem>
									</ul>
								</NavigationMenuContent>
							</NavigationMenuItem>
							<NavigationMenuItem>
								<NavigationMenuTrigger>Components</NavigationMenuTrigger>
								<NavigationMenuContent>
									<ul className="grid w-[400px] gap-3 p-4 md:w-[500px] md:grid-cols-2 lg:w-[600px] ">
										{components.map((component) => (
											<ListItem
												key={component.title}
												title={component.title}
												href={component.href}
											>
												{component.description}
											</ListItem>
										))}
									</ul>
								</NavigationMenuContent>
							</NavigationMenuItem>
							<NavigationMenuItem>
								<Link href="/docs" legacyBehavior passHref>
									<NavigationMenuLink className={navigationMenuTriggerStyle()}>
										Documentation
									</NavigationMenuLink>
								</Link>
							</NavigationMenuItem>
						</NavigationMenuList>
					</NavigationMenu>
				</div>
			</div>
			<div className="basis-1/5"></div>
		</div>
	);
}

const ListItem = React.forwardRef<
	React.ElementRef<"a">,
	React.ComponentPropsWithoutRef<"a">
>(({ className, title, children, ...props }, ref) => {
	return (
		<li>
			<NavigationMenuLink asChild>
				<a
					ref={ref}
					className={cn(
						"block select-none space-y-1 rounded-md p-2 pb-1 leading-none no-underline outline-none transition-colors hover:bg-accent hover:text-accent-foreground focus:bg-accent focus:text-accent-foreground",
						className,
					)}
					{...props}
				>
					<b className="text-base font-bold leading-none">{title}</b>
					<p className="text-sm">{children}</p>
				</a>
			</NavigationMenuLink>
		</li>
	);
});
ListItem.displayName = "ListItem";
