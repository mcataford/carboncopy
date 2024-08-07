# carboncopy

Keep your repositories up-to-date with their templates in a few keystrokes.

> # ✈️ Moved away!
>
> This project has moved away from Github and is now hosted [elsewhere](https://forge.karnov.club/marc/carboncopy).


![CarbonCopy CICD](https://github.com/mcataford/carboncopy/workflows/CarbonCopy%20CICD/badge.svg) ![PyPi version](https://img.shields.io/pypi/v/carboncopy) ![Wheel](https://img.shields.io/pypi/wheel/carboncopy) ![License](https://img.shields.io/pypi/l/carboncopy) ![Status](https://img.shields.io/pypi/status/carboncopy) 

## ❓ Why `carboncopy`?

[Github Template Repositories](https://github.blog/2019-06-06-generate-new-repositories-with-repository-templates/) made it really easy to skip project boilerplate setup steps and to produce "new project kits" that ensure that all your (or your organization's) new projects have all the must-haves. Problem is, templates aren't set in stone and it's likely that templates get updated after some projects have been spawned from it.

Because template repositories are different than forks, you can't simply rebase your project to gulp in the latest templated goodies -- leaving you with the gnarly task of manually moving files over. No more.

With `carboncopy`, you are one command away from pulling in the latest changes from your template repositories as if it were a regular base branch. You can configure it via its RC file to ignore certain files from the template, and more!

## 📦 Installation

It's easy as 1, 2, 3!

```
pip install carboncopy
```

## 🔨 Usage

From your repository, simply type `carboncopy` in your terminal to bring up a prompt asking you what to pull from your template repository. __Any change made is left as an unstaged change so you can commit and merge it however you want.__

## ⚙ Configuration

You can configure the way `carboncopy` handles your template's contents by creating a `.carboncopyrc` file at the root of your repository. Documentation TBD. See `src/carboncopy/config_defaults.py` for general layout.
