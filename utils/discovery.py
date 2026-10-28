import importlib
import logging
import pkgutil
import sys

logger = logging.getLogger(__name__)


def discover_game_objects(package_name: str) -> int:
    logger.info("Starting game objects auto-discovery in package: '%s'", package_name)

    try:
        package = importlib.import_module(package_name)
    except ModuleNotFoundError:
        logger.error("Failed to discover game objects: Package '%s' not found.", package_name)
        raise

    package_path = getattr(package, "__path__", None)
    if not package_path:
        logger.warning("Package '%s' has no __path__ attribute (is it a valid package?).", package_name)
        return 0

    imported_count = 0
    failed_count = 0

    for _, module_name, is_pkg in pkgutil.walk_packages(package_path, prefix=f"{package_name}."):
        if is_pkg:
            continue

        short_name = module_name.split(".")[-1]
        if short_name.startswith("_"):
            logger.debug("Skipping private module: '%s'", module_name)
            continue

        try:
            if module_name in sys.modules:
                logger.debug("Module '%s' is already loaded.", module_name)
            else:
                importlib.import_module(module_name)
                logger.debug("Successfully imported module: '%s'", module_name)

            imported_count += 1

        except Exception as err:
            failed_count += 1
            logger.error(
                "Failed to import game object module '%s': %s",
                module_name,
                err,
                exc_info=True,
            )

    logger.info(
        "Auto-discovery completed for '%s'. Imported: %d, Failed: %d.",
        package_name,
        imported_count,
        failed_count,
    )

    if failed_count > 0:
        logger.warning(
            "Auto-discovery finished with %d failure(s). Check logs above for details.",
            failed_count,
        )

    return imported_count
