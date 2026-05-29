//! Runtime distribution policy.
//!
//! The install/runtime code is generic. Values in this module come from the
//! runtime data block stamped onto each generated distribution artifact.

use std::path::PathBuf;

use crate::runtime_data;

pub(crate) fn command_name() -> &'static str {
    &runtime_data::current().header.command_name
}

pub(crate) fn embedded_command_name() -> &'static str {
    &runtime_data::current().header.embedded_command_name
}

pub(crate) fn display_name() -> &'static str {
    &runtime_data::current().header.display_name
}

pub(crate) fn default_prefix_dir() -> &'static str {
    &runtime_data::current().header.default_prefix_dir
}

pub(crate) fn metadata_file() -> &'static str {
    &runtime_data::current().header.metadata_file
}

pub(crate) fn bundle_env_var() -> &'static str {
    &runtime_data::current().header.bundle_env_var
}

pub(crate) fn offline_env_var() -> &'static str {
    &runtime_data::current().header.offline_env_var
}

pub(crate) fn docs_url() -> &'static str {
    &runtime_data::current().header.docs_url
}

pub(crate) fn default_prefix() -> miette::Result<PathBuf> {
    let home =
        dirs::home_dir().ok_or_else(|| miette::miette!("could not determine home directory"))?;
    Ok(home.join(default_prefix_dir()))
}

pub(crate) fn status_binary_name(has_embedded_bundle: bool) -> &'static str {
    if has_embedded_bundle {
        embedded_command_name()
    } else {
        command_name()
    }
}

pub(crate) fn frozen_message() -> String {
    format!(
        "This base environment is managed by {display}.\n\
Create a new environment instead: conda create -n myenv\n\
To re-bootstrap: {command} bootstrap --force\n\
To override: pass --override-frozen-env",
        display = display_name(),
        command = command_name()
    )
}
