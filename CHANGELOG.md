## [0.0.5] - August 24th, 2022

- Fix redux master store state was not being maintained correctly on @Redux.action resulting in the same state being use across all browser sessions.

## [0.0.4] - July 22nd, 2022

- Fix @callback *prevent_initial_call* argument default value clash

## [0.0.3] - June 12th, 2022

- Remove master store timestamp reference in surrogate merge callback as it triggers an an
unnecessary event.

## [0.0.2] - May 26th, 2022

- Make the master_store (dcc.Store) ID accessible from the container
- Added pytest button_test

## [0.0.1] - May 19th, 2022

- Initial release