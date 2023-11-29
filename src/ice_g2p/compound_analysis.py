"""
Decomposes compound words on a grapheme basis to prepare for automatic transcription.
"""

from ice_g2p import tree_builder
from ice_g2p import entry


def get_compound_parts(token: str) -> list:
    """ Decomposes 'token' if it is a compound.
    Returns a list of the components, or a single element list containing 'token'
    if no decomposition can be performed. """

    token_entry = entry.PronDictEntry(word=token)
    compound_tree = tree_builder.build_compound_tree_token_only(token_entry)
    result_arr = []
    decompose(compound_tree, result_arr)
    return result_arr


def decompose(entry_tree: tree_builder.CompoundTree, token_arr: list):
    """ Recursively call decompose on each element of entry_tree.
    Collects found compound elements as strings in 'token_arr'.
    """
    if not entry_tree.left:
        token_arr.append(entry_tree.elem.word)
    if entry_tree.left:
        decompose(entry_tree.left, token_arr)
    if entry_tree.right:
        decompose(entry_tree.right, token_arr)


